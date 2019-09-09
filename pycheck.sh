    #!/bin/sh
     
    echo "======  pycodestyle  ======"
    pycodestyle $1
    echo "======  pyflakes  ======"
    pyflakes $1
    echo "======  pylint  ======"
    pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --reports=n $1
    pylint -f parseable -r n $1

