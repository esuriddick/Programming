from .dds_importer import dds_importer

Krita.instance().addExtension(dds_importer(Krita.instance()))