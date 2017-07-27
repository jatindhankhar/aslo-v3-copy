FROM fedora:26

RUN dnf install -y git gettext sugar-toolkit-gtk3 sugar-toolkit

VOLUME /activity
WORKDIR /activity

CMD python /activity/setup.py dist_xo; \
    chmod 777 -R /activity/
