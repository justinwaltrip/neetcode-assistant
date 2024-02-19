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
  env.LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib/";  # required pymilvus to import cleanly
}
