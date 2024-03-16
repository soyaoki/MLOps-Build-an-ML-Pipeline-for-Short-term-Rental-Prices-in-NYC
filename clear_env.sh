for i in `conda env list | awk '{print $1}' | grep 'mlflow' | tr '\n' ' '`;do echo $i; conda env remove --name $i; done
