"""
Approximation
"""

from typing import List

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline


class Approximation:
    """
    Approximation
    """

    @classmethod
    def fit(cls,
            arguments: List[List[float]],
            results: List[float],
            degree: int = 2,
            ) -> "Approximation":
        """
        Fit the model

        :param arguments: Function arguments
        :param results: Function results
        :param degree: The degree of the polynomial features
        :return: Approximation
        """
        model = Pipeline([
            ("poly", PolynomialFeatures(degree)),
            ("linear", LinearRegression(fit_intercept=False)),
        ])
        model.fit(arguments, results)
        return cls(model)

    def __init__(self, model: Pipeline):
        """
        Constructor

        :param model: Model
        """
        self.__model = model
        self.__names = model.named_steps["poly"].get_feature_names()
        self.__coef = model.named_steps["linear"].coef_.tolist()
        self.__json = None
        self.__latex = None

    @property
    def names(self) -> List[str]:
        """
        Raw names
        """
        return self.__names

    @property
    def coef(self) -> List[float]:
        """
        Raw coefficients
        """
        return self.__coef

    @property
    def json(self) -> List[dict]:
        """
        Polynomial in JSON format
        """
        if self.__json is not None:
            return self.__json
        self.__json = []
        for i in range(len(self.names)):
            if self.coef[i] == 0:
                continue
            multipliers = {
                "coef": self.coef[i],
                "variables": [],
            }
            if self.names[i] != "1":
                for name in self.names[i].split(" "):
                    split_by_pow = name.split("^")
                    multipliers["variables"].append({
                        "index": int(split_by_pow[0][1:]) + 1,
                        "pow": int(split_by_pow[1]) if len(split_by_pow) == 2 else 1
                    })
            self.__json.append(multipliers)
        return self.__json

    @property
    def latex(self) -> str:
        """
         Polynomial in Latex format
        """
        if self.__latex is not None:
            return self.__latex
        self.__latex = []
        for multipliers in self.json:
            self.__latex.append(Approximation.__latex_format_coef(multipliers["coef"]))
            for variable in multipliers["variables"]:
                self.__latex.append(Approximation.__latex_format_variable(variable))
        self.__latex = "".join(self.__latex)
        if self.__latex.startswith("+"):
            self.__latex = self.__latex[1:]
        return self.__latex

    @staticmethod
    def __latex_format_coef(value: float) -> str:
        result = f"{value:+}"
        # split_by_e = result.split("e")
        # if len(split_by_e) == 2:
        #     result = f"{split_by_e[0]}\\mathrm{{e}}\\text{{{split_by_e[1]}}}"
        return result

    @staticmethod
    def __latex_format_variable(variable: dict) -> str:
        result = f"x_{Approximation.__latex_format_parentheses(variable['index'])}"
        if variable["pow"] != 1:
            result += f"^{Approximation.__latex_format_parentheses(variable['pow'])}"
        return result

    @staticmethod
    def __latex_format_parentheses(value: float) -> str:
        return f"{{{value}}}" if value > 9 else f"{value}"
