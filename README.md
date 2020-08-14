This is a app that can model the Hallam Nuclear Power Facility

It is based on the 1964 startup tests and models. 

Interestingly, they thought it had a negative power coeff but
in reality it hadn't. Maybe with better models we can 
actually predict that it's positive, and maybe we can
adjust it?

# Quick start

To install this app and run the analysis, first get the code:

    git clone https://github.com/ntouran/happ.git
    git submodule init --update

Then get some Hallam input files (info coming soon).

Then run the analysis locally:

    python -m happ run hallam.yaml

Or remotely by syncing to a shared drive:

    robocopy /mt /NP /NFL /NDL /s /mir . P:\ntouran\happ

And then submitting. In a Windows HPC (rare), you use:

    job submit /stdout:hallam.stdout /stderr:hallam.stderr /numprocessors:12 /jobname:Hallam /scheduler:hpcname /workdir:\\path\to\your\\hallam mpiexec -n 12 \\path\to\\Python.exe path\to\happ\happ run hallam.yaml

