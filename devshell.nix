{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShellNoCC {

  packages = with pkgs; [
    kubernetes-helm
    yaml-language-server
  ];

   shellHook = ''
    export SHELL='${pkgs.bashInteractive}/bin/bash'
  '';
}
