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
    ruff.enable = true;
  };
  enterShell = "pip install --upgrade pip";
  env.LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib/";  # required for python packages to import cleanly
}
