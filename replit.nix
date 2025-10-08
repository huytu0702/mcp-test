{ pkgs }: {
  deps = [
    pkgs.nodejs-18_x
  ];

  env = {
    PORT = "3000";
  };
}
