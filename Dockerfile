# basé sur Debian 12.1 (Bookworm)
FROM python:3.10

# Doit recevoir le "user identifier" en argument.
ARG UID
# Doit recevoir le "group identifier" en argument.
ARG GID

# Met à jour la liste des paquets, installe sudo, crée un utilisateur non-root et accorde l'accès à sudo sans mot de passe.
RUN apt update && \
    apt install -y sudo && \
    rm -rf /var/lib/apt/lists/* && \
    addgroup --gid $GID nonroot && \
    adduser --uid $UID --gid $GID --disabled-password --gecos "" nonroot && \
    echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

USER nonroot
WORKDIR /home/nonroot

# Crée un environnement virtuel pour Python.
# Pas nécessaire de le faire dans un conteneur Docker, mais cela donne les étapes à suivre si l'on veut recréer un environnement 
# similaire sans utiliser un environnement conteneurisée.
ENV VIRTUAL_ENV=/home/nonroot/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m venv venv && \
    . venv/bin/activate

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /home/nonroot/app

CMD ["/bin/bash"]
