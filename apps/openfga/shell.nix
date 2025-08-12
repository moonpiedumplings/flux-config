with import <nixpkgs> {};

mkShell {
  buildInputs = [
    openfga-cli
    nushell
    yq
    busybox
    jq
  ];

  shellHook = ''
    . <(fga completion bash)

    export FGA_API_URL="https://openfga.moonpiedumpl.ing"

    export FGA_API_TOKEN=$(kubectl get secrets -n openfga openfga-secrets -o jsonpath='{.data.values\.yaml}' | base64 -d | yq '.authn.preshared.keys.[0]' | sed 's/"//g') 

    export FGA_STORE_ID=$(fga store list | jq '.stores.[0].id' | sed 's/"//g')  
  '';
}
