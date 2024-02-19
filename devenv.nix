{ pkgs, ... }:

{
  packages = with pkgs; [
    awscli2
    docker
    nvidia-docker
    docker-compose
  ];
  languages.python = {
    enable = true;
    venv.enable = true;
    venv.requirements = ./requirements.txt;
  };
  pre-commit.hooks = {
    black.enable = true;
  };
  enterShell = "pip install --upgrade pip";
}
