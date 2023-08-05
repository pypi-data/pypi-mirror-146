# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyArgs',
    'GoogleCloudRecommendationengineV1beta1FeatureMapArgs',
    'GoogleCloudRecommendationengineV1beta1ImageArgs',
    'GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceArgs',
    'GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeArgs',
    'GoogleCloudRecommendationengineV1beta1ProductCatalogItemArgs',
]

@pulumi.input_type
class GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyArgs:
    def __init__(__self__, *,
                 categories: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        Category represents catalog item category hierarchy.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] categories: Catalog item categories. Each category should be a UTF-8 encoded string with a length limit of 2 KiB. Note that the order in the list denotes the specificity (from least to most specific).
        """
        pulumi.set(__self__, "categories", categories)

    @property
    @pulumi.getter
    def categories(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Catalog item categories. Each category should be a UTF-8 encoded string with a length limit of 2 KiB. Note that the order in the list denotes the specificity (from least to most specific).
        """
        return pulumi.get(self, "categories")

    @categories.setter
    def categories(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "categories", value)


@pulumi.input_type
class GoogleCloudRecommendationengineV1beta1FeatureMapArgs:
    def __init__(__self__, *,
                 categorical_features: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 numerical_features: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        FeatureMap represents extra features that customers want to include in the recommendation model for catalogs/user events as categorical/numerical features.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] categorical_features: Categorical features that can take on one of a limited number of possible values. Some examples would be the brand/maker of a product, or country of a customer. Feature names and values must be UTF-8 encoded strings. For example: `{ "colors": {"value": ["yellow", "green"]}, "sizes": {"value":["S", "M"]}`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] numerical_features: Numerical features. Some examples would be the height/weight of a product, or age of a customer. Feature names must be UTF-8 encoded strings. For example: `{ "lengths_cm": {"value":[2.3, 15.4]}, "heights_cm": {"value":[8.1, 6.4]} }`
        """
        if categorical_features is not None:
            pulumi.set(__self__, "categorical_features", categorical_features)
        if numerical_features is not None:
            pulumi.set(__self__, "numerical_features", numerical_features)

    @property
    @pulumi.getter(name="categoricalFeatures")
    def categorical_features(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Categorical features that can take on one of a limited number of possible values. Some examples would be the brand/maker of a product, or country of a customer. Feature names and values must be UTF-8 encoded strings. For example: `{ "colors": {"value": ["yellow", "green"]}, "sizes": {"value":["S", "M"]}`
        """
        return pulumi.get(self, "categorical_features")

    @categorical_features.setter
    def categorical_features(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "categorical_features", value)

    @property
    @pulumi.getter(name="numericalFeatures")
    def numerical_features(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Numerical features. Some examples would be the height/weight of a product, or age of a customer. Feature names must be UTF-8 encoded strings. For example: `{ "lengths_cm": {"value":[2.3, 15.4]}, "heights_cm": {"value":[8.1, 6.4]} }`
        """
        return pulumi.get(self, "numerical_features")

    @numerical_features.setter
    def numerical_features(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "numerical_features", value)


@pulumi.input_type
class GoogleCloudRecommendationengineV1beta1ImageArgs:
    def __init__(__self__, *,
                 uri: pulumi.Input[str],
                 height: Optional[pulumi.Input[int]] = None,
                 width: Optional[pulumi.Input[int]] = None):
        """
        Catalog item thumbnail/detail image.
        :param pulumi.Input[str] uri: URL of the image with a length limit of 5 KiB.
        :param pulumi.Input[int] height: Optional. Height of the image in number of pixels.
        :param pulumi.Input[int] width: Optional. Width of the image in number of pixels.
        """
        pulumi.set(__self__, "uri", uri)
        if height is not None:
            pulumi.set(__self__, "height", height)
        if width is not None:
            pulumi.set(__self__, "width", width)

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Input[str]:
        """
        URL of the image with a length limit of 5 KiB.
        """
        return pulumi.get(self, "uri")

    @uri.setter
    def uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "uri", value)

    @property
    @pulumi.getter
    def height(self) -> Optional[pulumi.Input[int]]:
        """
        Optional. Height of the image in number of pixels.
        """
        return pulumi.get(self, "height")

    @height.setter
    def height(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "height", value)

    @property
    @pulumi.getter
    def width(self) -> Optional[pulumi.Input[int]]:
        """
        Optional. Width of the image in number of pixels.
        """
        return pulumi.get(self, "width")

    @width.setter
    def width(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "width", value)


@pulumi.input_type
class GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceArgs:
    def __init__(__self__, *,
                 display_price: Optional[pulumi.Input[float]] = None,
                 original_price: Optional[pulumi.Input[float]] = None):
        """
        Exact product price.
        :param pulumi.Input[float] display_price: Optional. Display price of the product.
        :param pulumi.Input[float] original_price: Optional. Price of the product without any discount. If zero, by default set to be the 'displayPrice'.
        """
        if display_price is not None:
            pulumi.set(__self__, "display_price", display_price)
        if original_price is not None:
            pulumi.set(__self__, "original_price", original_price)

    @property
    @pulumi.getter(name="displayPrice")
    def display_price(self) -> Optional[pulumi.Input[float]]:
        """
        Optional. Display price of the product.
        """
        return pulumi.get(self, "display_price")

    @display_price.setter
    def display_price(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "display_price", value)

    @property
    @pulumi.getter(name="originalPrice")
    def original_price(self) -> Optional[pulumi.Input[float]]:
        """
        Optional. Price of the product without any discount. If zero, by default set to be the 'displayPrice'.
        """
        return pulumi.get(self, "original_price")

    @original_price.setter
    def original_price(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "original_price", value)


@pulumi.input_type
class GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeArgs:
    def __init__(__self__, *,
                 max: pulumi.Input[float],
                 min: pulumi.Input[float]):
        """
        Product price range when there are a range of prices for different variations of the same product.
        :param pulumi.Input[float] max: The maximum product price.
        :param pulumi.Input[float] min: The minimum product price.
        """
        pulumi.set(__self__, "max", max)
        pulumi.set(__self__, "min", min)

    @property
    @pulumi.getter
    def max(self) -> pulumi.Input[float]:
        """
        The maximum product price.
        """
        return pulumi.get(self, "max")

    @max.setter
    def max(self, value: pulumi.Input[float]):
        pulumi.set(self, "max", value)

    @property
    @pulumi.getter
    def min(self) -> pulumi.Input[float]:
        """
        The minimum product price.
        """
        return pulumi.get(self, "min")

    @min.setter
    def min(self, value: pulumi.Input[float]):
        pulumi.set(self, "min", value)


@pulumi.input_type
class GoogleCloudRecommendationengineV1beta1ProductCatalogItemArgs:
    def __init__(__self__, *,
                 available_quantity: Optional[pulumi.Input[str]] = None,
                 canonical_product_uri: Optional[pulumi.Input[str]] = None,
                 costs: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 currency_code: Optional[pulumi.Input[str]] = None,
                 exact_price: Optional[pulumi.Input['GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceArgs']] = None,
                 images: Optional[pulumi.Input[Sequence[pulumi.Input['GoogleCloudRecommendationengineV1beta1ImageArgs']]]] = None,
                 price_range: Optional[pulumi.Input['GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeArgs']] = None,
                 stock_state: Optional[pulumi.Input['GoogleCloudRecommendationengineV1beta1ProductCatalogItemStockState']] = None):
        """
        ProductCatalogItem captures item metadata specific to retail products.
        :param pulumi.Input[str] available_quantity: Optional. The available quantity of the item.
        :param pulumi.Input[str] canonical_product_uri: Optional. Canonical URL directly linking to the item detail page with a length limit of 5 KiB..
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] costs: Optional. A map to pass the costs associated with the product. For example: {"manufacturing": 45.5} The profit of selling this item is computed like so: * If 'exactPrice' is provided, profit = displayPrice - sum(costs) * If 'priceRange' is provided, profit = minPrice - sum(costs)
        :param pulumi.Input[str] currency_code: Optional. Only required if the price is set. Currency code for price/costs. Use three-character ISO-4217 code.
        :param pulumi.Input['GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceArgs'] exact_price: Optional. The exact product price.
        :param pulumi.Input[Sequence[pulumi.Input['GoogleCloudRecommendationengineV1beta1ImageArgs']]] images: Optional. Product images for the catalog item.
        :param pulumi.Input['GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeArgs'] price_range: Optional. The product price range.
        :param pulumi.Input['GoogleCloudRecommendationengineV1beta1ProductCatalogItemStockState'] stock_state: Optional. Online stock state of the catalog item. Default is `IN_STOCK`.
        """
        if available_quantity is not None:
            pulumi.set(__self__, "available_quantity", available_quantity)
        if canonical_product_uri is not None:
            pulumi.set(__self__, "canonical_product_uri", canonical_product_uri)
        if costs is not None:
            pulumi.set(__self__, "costs", costs)
        if currency_code is not None:
            pulumi.set(__self__, "currency_code", currency_code)
        if exact_price is not None:
            pulumi.set(__self__, "exact_price", exact_price)
        if images is not None:
            pulumi.set(__self__, "images", images)
        if price_range is not None:
            pulumi.set(__self__, "price_range", price_range)
        if stock_state is not None:
            pulumi.set(__self__, "stock_state", stock_state)

    @property
    @pulumi.getter(name="availableQuantity")
    def available_quantity(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. The available quantity of the item.
        """
        return pulumi.get(self, "available_quantity")

    @available_quantity.setter
    def available_quantity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "available_quantity", value)

    @property
    @pulumi.getter(name="canonicalProductUri")
    def canonical_product_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Canonical URL directly linking to the item detail page with a length limit of 5 KiB..
        """
        return pulumi.get(self, "canonical_product_uri")

    @canonical_product_uri.setter
    def canonical_product_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "canonical_product_uri", value)

    @property
    @pulumi.getter
    def costs(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Optional. A map to pass the costs associated with the product. For example: {"manufacturing": 45.5} The profit of selling this item is computed like so: * If 'exactPrice' is provided, profit = displayPrice - sum(costs) * If 'priceRange' is provided, profit = minPrice - sum(costs)
        """
        return pulumi.get(self, "costs")

    @costs.setter
    def costs(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "costs", value)

    @property
    @pulumi.getter(name="currencyCode")
    def currency_code(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. Only required if the price is set. Currency code for price/costs. Use three-character ISO-4217 code.
        """
        return pulumi.get(self, "currency_code")

    @currency_code.setter
    def currency_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "currency_code", value)

    @property
    @pulumi.getter(name="exactPrice")
    def exact_price(self) -> Optional[pulumi.Input['GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceArgs']]:
        """
        Optional. The exact product price.
        """
        return pulumi.get(self, "exact_price")

    @exact_price.setter
    def exact_price(self, value: Optional[pulumi.Input['GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceArgs']]):
        pulumi.set(self, "exact_price", value)

    @property
    @pulumi.getter
    def images(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GoogleCloudRecommendationengineV1beta1ImageArgs']]]]:
        """
        Optional. Product images for the catalog item.
        """
        return pulumi.get(self, "images")

    @images.setter
    def images(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GoogleCloudRecommendationengineV1beta1ImageArgs']]]]):
        pulumi.set(self, "images", value)

    @property
    @pulumi.getter(name="priceRange")
    def price_range(self) -> Optional[pulumi.Input['GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeArgs']]:
        """
        Optional. The product price range.
        """
        return pulumi.get(self, "price_range")

    @price_range.setter
    def price_range(self, value: Optional[pulumi.Input['GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeArgs']]):
        pulumi.set(self, "price_range", value)

    @property
    @pulumi.getter(name="stockState")
    def stock_state(self) -> Optional[pulumi.Input['GoogleCloudRecommendationengineV1beta1ProductCatalogItemStockState']]:
        """
        Optional. Online stock state of the catalog item. Default is `IN_STOCK`.
        """
        return pulumi.get(self, "stock_state")

    @stock_state.setter
    def stock_state(self, value: Optional[pulumi.Input['GoogleCloudRecommendationengineV1beta1ProductCatalogItemStockState']]):
        pulumi.set(self, "stock_state", value)


