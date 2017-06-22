FROM fedora:22

RUN dnf install -y git gettext

RUN git clone --depth=1 https://github.com/sugarlabs/sugar-toolkit-gtk3; \
    mv sugar-toolkit-gtk3/src/sugar3 /usr/lib/python2.7/site-packages/sugar3; \
    rm -rf sugar-toolkit-gtk3

RUN rm -rf /usr/lib/python2.7/site-packages/sugar; \
    ln -s /usr/lib/python2.7/site-packages/sugar3 /usr/lib/python2.7/site-packages/sugar

VOLUME /activity
WORKDIR /activity

CMD python /activity/setup.py dist_xo --no-fail; \
    chmod 777 -R /activity/
