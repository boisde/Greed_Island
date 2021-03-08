#!/usr/bin/python3
import logging
import os
import pathlib

import envyaml


def load_env(env_yaml_path='env.yaml'):
    env_path = pathlib.Path(env_yaml_path)
    if env_path.exists():
        logging.info("Loading from [%s]." % env_path)
        # read file env.yaml and parse config
        env = envyaml.EnvYAML(env_path, strict=False)
        for k in env.keys():
            level_one_val = env.get(k)
            if type(level_one_val) == str:
                os.environ[k] = level_one_val
            else:
                logging.error("Can't parse leveled values!")
                return


if __name__ == '__main__':
    # Load env from env.yaml file if exists (local-run only).
    load_env()
    web3_infura_project_id = os.environ.get('WEB3_INFURA_PROJECT_ID')
    private_key = os.environ.get('PRIVATE_KEY')

    # Generate
    with open('export_env.sh', 'w+') as f:
        lines = [
            "#!/usr/bin/env bash",
            "",
            "# RUN me with sourcing in terminal: i.e. `. ./export_env.sh`",
            f"export WEB3_INFURA_PROJECT_ID=\"{web3_infura_project_id}\"",
            f"export PRIVATE_KEY=\"{private_key}\"",
            "echo \"echo \\$WEB3_INFURA_PROJECT_ID\"",
            "echo \"echo \\$PRIVATE_KEY\"",
        ]
        for line in lines:
            f.write(line + '\n')

    print('Generated bash script for env var setting.')
    print('Next, run with `. ./export_env.sh`.')
