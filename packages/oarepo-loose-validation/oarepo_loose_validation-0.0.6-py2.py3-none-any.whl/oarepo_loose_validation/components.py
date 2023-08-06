from invenio_records_resources.services.records.components import ServiceComponent


class LooseValidationComponent(ServiceComponent):
    """Service component for metadata."""

    def create(self, identity, data=None, record=None, errors=None, **kwargs):
        """Inject parsed metadata to the record."""
        record.validace = data.get('validace', {})

    def update(self, identity, data=None, record=None, **kwargs):
        """Inject parsed metadata to the record."""
        record.validace = data.get('validace', {})
