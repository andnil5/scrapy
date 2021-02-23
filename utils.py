import os

def log_to_file(data, filename):
    """Logs branch coverage result to the given file in the `branch_cov_logs` directory."""
    log_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'branch_cov_logs')
    file = os.path.join(log_dir, filename)
    with open(file, 'w+') as f:
        f.write("Coverage: {:.2f}%\n".format(sum(data)/len(data)*100))
        f.write("{}\n".format(str(data)))