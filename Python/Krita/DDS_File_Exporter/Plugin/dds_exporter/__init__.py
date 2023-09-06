from .dds_exporter import dds_exporter

Krita.instance().addExtension(dds_exporter(Krita.instance()))