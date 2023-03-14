## Задание 1

Внутри папки docker_1:

```
docker image build . --tag=dz1
```

```
docker run --name=dz1_run -p 7007:80 -d dz1
```

## Задание 2

Внутри папки docker_2:

```
docker image build . --tag=dz2
```

```
docker run --name=dz2_run -p 7007:6060 -d dz2
```
