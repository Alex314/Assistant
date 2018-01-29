def get_command_list():
    return 'exec', 'self.q_out.put([t.example for t in self.possible_tasks])'
