
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
from uuid import uuid4, UUID


@dataclass
class LaptopSpecification:
    company: str
    product: str
    type_name: str
    screen_size: float
    screen_resolution: str
    cpu: str
    ram: int
    gpu: str
    operating_system: str
    weight: float


@dataclass
class PricePrediction:
    predicted_price: float
    currency: str = "USD"
    confidence_interval: Optional[tuple] = None

    def convert_currency(self, target_currency: str, conversion_rate: float) -> "PricePrediction":
        return PricePrediction(
            predicted_price=self.predicted_price * conversion_rate,
            currency=target_currency,
            confidence_interval=self.confidence_interval
        )


@dataclass
class LaptopCategory:
    name: str
    description: str

    @classmethod
    def categorize(cls, specs: LaptopSpecification, price: float) -> "LaptopCategory":
        if "gaming" in specs.type_name.lower() or "gaming" in specs.product.lower():
            return cls(name="Gaming", description="Designed for high-performance gaming")
        elif price > 1500 or "premium" in specs.product.lower():
            return cls(name="Premium", description="High-end performance and build quality")
        elif price < 700:
            return cls(name="Budget", description="Affordable with basic functionality")
        else:
            return cls(name="Mainstream", description="Good balance of performance and price")


@dataclass
class PredictionHistory:
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
    specification: LaptopSpecification = None
    price_prediction: PricePrediction = None
    category: LaptopCategory = None


@dataclass
class RecommendedLaptop:
    company: str
    product: str
    specifications: LaptopSpecification
    actual_price: float
    similarity_score: float


@dataclass
class LaptopComparison:
    laptops: List[RecommendedLaptop]
    comparison_attributes: Dict[str, List] = field(default_factory=dict)

    def add_laptop(self, laptop: RecommendedLaptop):
        self.laptops.append(laptop)
        for key, value in laptop.specifications.__dict__.items():
            if key not in self.comparison_attributes:
                self.comparison_attributes[key] = []
            self.comparison_attributes[key].append(value)
