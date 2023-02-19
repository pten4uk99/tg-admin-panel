class MockGenerator:
    fields: dict

    def __init__(self):
        assert self.fields is not None, 'Обязательный атрибут "fields"'
        self.fields = self.fields.copy()

    def __str__(self):
        return self.fields

    def update(self, **kwargs):
        self.fields.update(kwargs)
        return self

    async def _create_object(self):
        """ Непосредственно создает объект в БД """

        raise NotImplementedError()

    async def generate_mock_data(self, quantity: int = 1):
        """
        Добавляет данные в БД.
        quantity - необходимое количество созданных объектов
        """

        for i in range(quantity):
            await self._create_object()
