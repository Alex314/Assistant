def get_command_list():
    return 'exec', 'self.q_out.put([t.example for t in self.possible_tasks])'


def get_active_processes():
    return 'exec', 'self.q_out.put(["Active processes:"] + [pr.name for pr in active_children()])'
