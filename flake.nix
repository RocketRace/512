{
  description = "A game of 512";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (sys:
    let
      pkgs = nixpkgs.legacyPackages.${sys};
      crate = pkgs.rustPlatform.buildRustPackage {
        pname = "512";
        version = "0.0.0";
        src = ./.;
        cargoLock = {
          lockFile = ./Cargo.lock;
          outputHashes = {
            "ti-1.2.0" = "243292b03ea547c575f9e9508e693b5b35389c27a2f95ce5951835cff8925857";
          };
        };
      };
    in {
      packages.default = crate;
      devShells.default = pkgs.mkShell {
        packages = [ crate ];
        env = {
            # Required for rust-analyzer to work for me. Maybe it's because
            # I've installed it through a vscode extensions overlay.
            RUST_SRC_PATH = "${pkgs.rustPlatform.rustLibSrc}";
          };
      };
    }
  );
}