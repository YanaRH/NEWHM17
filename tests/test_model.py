import pytest
from src.model import Product, Smartphone, LawnGrass, Category

@pytest.fixture()
def sample_smartphone():
    return Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, "High", "15", "512GB", "Gray")

@pytest.fixture()
def sample_lawn_grass():
    return LawnGrass("Green Lawn", "High-quality grass", 500.0, 100, "USA", "7 days", "Green")

@pytest.fixture()
def sample_category():
    return Category("Смартфоны", "Современные смартфоны с высокими характеристиками")

def test_check_smartphone(sample_smartphone):
    assert sample_smartphone.name == "Iphone 15"
    assert sample_smartphone.description == "512GB, Gray space"
    assert sample_smartphone.price == 210000.0
    assert sample_smartphone.quantity == 8
    assert sample_smartphone.efficiency == "High"
    assert sample_smartphone.model == "15"
    assert sample_smartphone.memory == "512GB"
    assert sample_smartphone.color == "Gray"

def test_check_lawn_grass(sample_lawn_grass):
    assert sample_lawn_grass.name == "Green Lawn"
    assert sample_lawn_grass.description == "High-quality grass"
    assert sample_lawn_grass.price == 500.0
    assert sample_lawn_grass.quantity == 100
    assert sample_lawn_grass.country == "USA"
    assert sample_lawn_grass.germination_period == "7 days"
    assert sample_lawn_grass.color == "Green"

def test_add_product(sample_category, sample_smartphone):
    sample_category.add_product(sample_smartphone)
    assert "Iphone 15, 15, 512GB, Gray, 210000.0 руб. Остаток: 8 шт." in sample_category.products
    assert Category.product_count == 1

def test_add_invalid_product(sample_category):
    with pytest.raises(TypeError):
        sample_category.add_product("Invalid Product")

def test_product_addition(sample_smartphone):
    smartphone2 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, "High", "S23 Ultra", "256GB", "Gray")
    result = sample_smartphone + smartphone2
    assert result == 210000.0 * 8 + 180000.0 * 5

def test_invalid_product_addition(sample_smartphone, sample_lawn_grass):
    with pytest.raises(TypeError):
        _ = sample_smartphone + sample_lawn_grass

def test_category_iteration(sample_category, sample_smartphone):
    smartphone2 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, "High", "S23 Ultra", "256GB", "Gray")
    sample_category.add_product(sample_smartphone)
    sample_category.add_product(smartphone2)

    products = [product for product in sample_category]
    assert len(products) == 2
    assert products[0] == sample_smartphone
    assert products[1] == smartphone2

def test_logging_mixin(capsys):
    product = Product("Test Product", "Description", 100.0, 10)
    captured = capsys.readouterr()
    assert "Создан объект Product с параметрами: ('Test Product', 'Description', 100.0, 10), {}" in captured.out

def test_zero_quantity_product():
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Test Product", "Description", 100.0, 0)

def test_average_price(sample_category, sample_smartphone):
    sample_category.add_product(sample_smartphone)
    smartphone2 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, "High", "S23 Ultra", "256GB", "Gray")
    sample_category.add_product(smartphone2)
    assert sample_category.average_price() == (210000.0 + 180000.0) / 2

def test_average_price_no_products(sample_category):
    assert sample_category.average_price() == 0
