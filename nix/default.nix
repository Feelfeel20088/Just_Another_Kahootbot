{pkgs}:
let 
  just_another_kahootbot = (with pkgs; python313Packages.buildPythonApplication {
    name = "just_another_kahootbot";
    version = "v0.2.0-alpha";

    src = ../.;

    propagatedBuildInputs = (with python313Packages; [
      httpx
      websockets
      quart
      pydantic
      orjson
    
    ]) ++ [
      nodejs
      python313
      npm
      
      rustc
      pkg-config
    ];
    
    postInstall = ''
      mkdir -p $out/app
      cp -r justAnotherKahootBot $out/app/
      
    '';
# rm -rf $out/justAnotherKahootBot
    meta = {
      description = "Just_Another_Kahoot_Bot is a highly scalable, single-threaded bot for Kahoot, built for deployment on Kubernetes. Unlike traditional bots that rely on Selenium, this bot uses raw WebSockets, providing better performance, stability, and reliability. The bot can flood Kahoot games, answer questions correctly, and remain stealthy.";
      homepage = "https://github.com/Feelfeel20088/Just_Another_Kahootbot";
      license = lib.licenses.gpl3Only;
      maintainers = with lib.maintainers; [ felix ];
    };
  });
in {
  inherit just_another_kahootbot;
}

    # postInstall = ''
    #   mkdir -p $out/app
    #   cp -r . $out/app/
    # '';