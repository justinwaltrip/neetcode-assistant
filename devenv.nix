{ pkgs, ... }:

{
  packages = [
    pkgs.awscli2
  ];
  languages.python = {
    enable = true;
    venv.enable = true;
    venv.requirements = ./requirements.txt;
  };
  pre-commit.hooks = {
    black.enable = true;
  };
}
