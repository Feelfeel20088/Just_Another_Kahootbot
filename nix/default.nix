{pkgs}: final: prev:
let 
  felixhub = (with pkgs; buildNpmPackage {
    pname = "felixhub-portfolio-site";
    version = "1.0";

    src = ../.;

    npmDepsHash = "sha256-ap2iD0tZnivycTiDLuFsCuGeXp+291DM/ljq3nh1to4=";

    npmPackFlags = [ "--ignore-scripts" ];

    NODE_OPTIONS = "--openssl-legacy-provider";

    buildInputs = [ typescript ];

    postInstall = ''
      mkdir -p $out/app
      cp -r . $out/app/
    '';

    meta = {
      description = "Portfolio website for Felix";
      homepage = "https://felixhub.dev";
      license = lib.licenses.gpl3Only;
      maintainers = with lib.maintainers; [ felix ];
    };
  });
in {
  inherit felixhub;
}