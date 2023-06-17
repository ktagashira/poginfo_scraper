FROM public.ecr.aws/lambda/python@sha256:70b056503bffcc49eefe22897782393a984efa04be670dfd7aec1351bea6717d as build
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1135561%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/

FROM public.ecr.aws/lambda/python@sha256:70b056503bffcc49eefe22897782393a984efa04be670dfd7aec1351bea6717d
RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y

COPY --from=build /opt/chrome-linux /opt/chrome
COPY --from=build /opt/chromedriver /opt/

COPY src/app.py ${LAMBDA_TASK_ROOT}
COPY ./pyproject.toml ${LAMBDA_TASK_ROOT}
COPY ./poetry.lock ${LAMBDA_TASK_ROOT}

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && echo 'export PATH="/root/.local/bin:$PATH"' >> ~/.bashrc \
    && source ~/.bashrc \
    && poetry config virtualenvs.create false \ 
    && poetry install --no-root --no-dev

CMD [ "app.handler" ]