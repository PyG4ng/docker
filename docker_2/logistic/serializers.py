from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']
    pass


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    # product = ProductSerializer()

    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']
    pass


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions_data = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = Stock.objects.create(**validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions_data:
            StockProduct.objects.create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        new_positions_data = validated_data.pop('positions')

        # обновляем склад по его параметрам
        # if instance.address != validated_data.get('address', instance.address):
        #     instance.address = validated_data.get('address', instance.address)
        #     instance.save()
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        positions_with_same_stock_pk = StockProduct.objects.filter(
            stock=instance.pk).values_list('product', flat=True)

        # for position in positions_with_same_stock_pk:
        position_product_pool = []
        for new_position in new_positions_data:
            if 'product' in new_position.keys():
                if StockProduct.objects.filter(stock=instance.pk).filter(product=new_position.get('product')).exists():
                    position = StockProduct.objects.filter(stock=instance.pk).get(
                        product=new_position.get('product'))
                    position.quantity = new_position.get(
                        'quantity', position.quantity)
                    position.price = new_position.get('price', position.price)
                    position.save()
                    position_product_pool.append(position.product.id)
                else:
                    position = StockProduct.objects.create(
                        stock=instance, **new_position)
                    position_product_pool.append(position.product.id)
        for product in positions_with_same_stock_pk:
            if product not in position_product_pool:
                StockProduct.objects.filter(stock=instance.pk).filter(
                    product=product).delete()

        return stock
