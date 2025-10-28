# System guidelines:
## System Info:
> uname -a 
> Linux alono-LOQ-15IRX10 6.14.0-33-generic #33~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Sep 19 17:02:30 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
> nvidia-smi
> NVIDIA-SMI 580.95.05              Driver Version: 580.95.05      CUDA Version: 13.0


## General guidelines
- Always prefer Python 3.12 or newer for scripts and tooling.
- For visualisation scripts (matplotlib, pandas, etc...) use micromamba environment visualisation.
- Check if micromamba environment exists for current project, if not create it and document it at project level CLAUDE.md
- Enforce PEP8 compliance across all codebases.
- Use my system timezone (Madrid Central) for all timestamps.
- Avoid storing secrets or credentials in code, ask the user to modify the .env files, just provide template.env.
- Avoid creating many markdown files. Maintain a complete and professional README.md, the rest of the documentation should be in the docs folder with an index.md that organises the structure of the documentation and ensure no files is above 500 lines. Ensure proper organisation in these subfolders.
- Ask me before guessing, enumerate questins and provide defaults. Group similar questions with subnumbners (x.y), assume questions I don't answer should be used with the default value you have given to me.

## Tools
- Default linter: flake8
- Default formatter: black
- Default test runner: pytest