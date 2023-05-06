from fabricius.events.signal import Signal

on_generator_file_add = Signal()

before_file_commit = Signal()
on_commit_fail = Signal()
after_file_commit = Signal()

before_template_commit = Signal()
after_template_commit = Signal()
