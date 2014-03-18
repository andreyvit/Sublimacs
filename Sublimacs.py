import sublime, sublime_plugin
import datetime

class ViewCommand(sublime_plugin.TextCommand):

    def run_(self, args):
        if args:
            if 'event' in args:
                del args['event']

            self.pre_run(**args)
            edit = self.view.begin_edit(self.name(), args)
            try:
                return self.run(edit, **args)
            finally:
                self.view.end_edit(edit)
                self.post_run()
        else:
            self.pre_run()
            edit = self.view.begin_edit(self.name())
            try:
                return self.run(edit)
            finally:
                self.view.end_edit(edit)
            self.post_run()

    def pre_run(self):
        pass

    def post_run(self):
        pass

class KillRing(object):
	def __init__(self):
		self.stack = []
		self.open = False
		self.yank_pos = None

	def _append(self, text):
		self.stack[-1] += text

	def _push(self, text):
		self.stack.append(text)

	def kill(self, text):
		if self.open:
			self._append(text)
		else:
			self._push(text)
			self.open = True

	def yank_first(self):
		if len(self.stack) == 0:
			return None
		self.yank_pos = 1
		return self.stack[-self.yank_pos]
	
	def yank_previous(self):
		if len(self.stack) == 0:
			return None
		if self.yank_pos is None:
			return None
		if self.yank_pos >= len(self.stack):
			self.yank_pos = 1
		else:
			self.yank_pos += 1
		return self.stack[-self.yank_pos]
	
	def yank_next(self):
		if len(self.stack) == 0:
			return None
		if self.yank_pos is None:
			return None
		if self.yank_pos <= 1:
			self.yank_pos = len(self.stack)
		else:
			self.yank_pos -= 1
		return self.stack[-self.yank_pos]

	def close(self):
		self.open = False
		
	def close_yank(self):
		self.yank_pos = None

class Emacs(object):
	def __init__(self):
		self.kill_ring = KillRing()
		self.autoflags = { 'killed_sel': False, 'killed_mod': False, 'yanked_mod': False }

	def region_to_act_on(self, view):
		region_set = view.sel()
		region = region_set[0]

		if region.empty():
			mark = view.get_regions("mark")
			if len(mark) == 0:
				return None
			another = mark[0]
			#print sublime.Region(region.begin(), another.begin())
			return sublime.Region(region.begin(), another.begin())
		else:
			return region

	def kill(self, view, edit, region):
		self.kill_ring.kill(view.substr(region))
		view.erase(edit, region)
		self.set_autoflag('killed_sel', 'killed_mod')

	def yank(self, view, edit, text):
		pos = view.sel()[0].b
		view.insert(edit, pos, text)

		end_pos = pos + len(text)
		view.sel().clear()
		view.sel().add(sublime.Region(end_pos, end_pos))

		self.set_autoflag('yanked_mod')

	def set_autoflag(self, *names):
		for name in names:
			old = self.autoflags[name]
			if old == False:
				self.autoflags[name] = True

				def end_func():
					self.autoflags[name] = False
				sublime.set_timeout(end_func, 50)

	def autoflag(self, name):
		val = self.autoflags[name]
		if val:
			self.autoflags[name] = False
		return val

emacs = Emacs()

class EmacsKillCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		region = emacs.region_to_act_on(self.view)
		if region is not None:
			emacs.kill(self.view, edit, region)

class EmacsSaveToKillRingCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		region = emacs.region_to_act_on(self.view)
		if region is not None:
			emacs.kill_ring.kill(self.view.substr(region))

class EmacsKillToEolCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		pos = self.view.sel()[0].b
		end = self.view.line(pos).end()
		if end == pos:
			end += 1

		region = sublime.Region(pos, end)
		emacs.kill(self.view, edit, region)		

class EmacsYankCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		text = emacs.kill_ring.yank_first()
		if text is not None:
			emacs.yank(self.view, edit, text)

class EmacsYankPreviousCommand(ViewCommand):
	def pre_run(self):
		self.text = emacs.kill_ring.yank_previous()
		if self.text is not None:
			emacs.set_autoflag('yanked_mod')
			self.view.run_command('undo')

	def run(self, edit):
		if self.text is not None:
			emacs.yank(self.view, edit, self.text)

class EmacsYankNextCommand(ViewCommand):
	def pre_run(self):
		self.text = emacs.kill_ring.yank_next()
		if self.text is not None:
			emacs.just_yanked = True
			self.view.run_command('undo')

	def run(self, edit):
		if self.text is not None:
			emacs.yank(self.view, edit, self.text)

class EmacsListener(sublime_plugin.EventListener):

	def on_selection_modified(self, view):
		# print "on_selection_modified"
		if not emacs.autoflag('killed_sel'):
			emacs.kill_ring.close()

	def on_modified(self, view):
		# print "modified"
		if not emacs.autoflag('killed_mod'):
			emacs.kill_ring.close()
		if not emacs.autoflag('yanked_mod'):
			emacs.kill_ring.close_yank()
