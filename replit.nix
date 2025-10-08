{
  pkgs,
  nodejs-18_x,
  ...
}: {
  name = "exchange-rates-mcp-server";

  deps = [
    nodejs-18_x
    pkgs.nodePackages.npm
  ];

  env = {
    PORT = "3000";
  };

  scripts = {
    start = ''
      npm install
      npm start
    '';
  };
}
