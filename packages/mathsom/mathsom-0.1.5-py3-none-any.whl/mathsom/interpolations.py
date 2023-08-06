from typing import Union, get_args
import numpy as np
from scipy.interpolate import CubicSpline
from collections.abc import Sequence
from enum import Enum
from multimethod import multimethod

class InterpolationMethod(Enum):
    LINEAR = 'linear'
    LOGLINEAR = 'loglinear'
    CUBIC_SPLINE = 'cubic_spline'


@multimethod
def _adapt_interpolation_result(x: Union[int, float, Sequence, np.ndarray], result: float) -> float:
    return result

@multimethod
def _adapt_interpolation_result(x: Union[int, float], result: Sequence) -> float:
    return result[0]

@multimethod
def _adapt_interpolation_result(x: Union[int, float], result: np.ndarray) -> float:
    return float(result)

@multimethod
def _adapt_interpolation_result(x: Union[Sequence, np.ndarray], result: Sequence) -> np.ndarray:
    return np.array(result)

@multimethod
def _adapt_interpolation_result(x: Union[Sequence, np.ndarray], result: np.ndarray) -> np.ndarray:
    return result

def adapt_interpolation_result(x: Union[float, Sequence, np.ndarray], result: Union[float, Sequence, np.ndarray]) -> Union[float, np.ndarray]:
    '''
    Adapts interpolation result to the input x. If input is Sequence, result will be adapted to np.ndarray, else result will be a float.
    ----------
    Parameters:
    ----
        x (Union[float, Sequence, np.ndarray]): Value(s) to be interpolated.
        result (Union[float, Sequence, np.ndarray]): Interpolated y(x) value(s).
    ----
    Returns:
    ----
        result (Union[float, np.ndarray]): Adapted interpolation result.
    '''
    return _adapt_interpolation_result(x, result)

def check_pairs_interpolation(x_input: Union[Sequence, np.ndarray], y_input: Union[Sequence, np.ndarray]) -> None:
    if len(x_input) != len(y_input):
        raise ValueError(f'x_input and y_input must have the same length. x_input: {len(x_input)}, y_input: {len(y_input)}')

def linear_interpolation(x: Union[float, Sequence, np.ndarray], known_xs: Union[Sequence, np.ndarray], known_ys: Union[Sequence, np.ndarray]) -> Union[float, np.ndarray]:
    '''
    Linear interpolation. Interpolates y(x) for a given number of pairs (x, y) received in 2 Sequence or np.ndarray of same length.
    ----------
    Parameters:
    ----
        x (Union[float, Sequence, np.ndarray]): Value(s) to be interpolated.
        known_xs (Union[Sequence, np.ndarray]): Sequence or np.ndarray of x values.
        known_ys (Union[Sequence, np.ndarray]): Sequence or np.ndarray of y values.
    ----
    Returns:
    ----
        result (Union[float, np.ndarray]): Interpolated y(x) value(s).
    '''
    result = np.interp(x, known_xs, known_ys)
    return result

def loglinear_interpolation(x, known_xs, known_ys):
    '''
    Log linear interpolation. Interpolates y(x) for a given number of pairs (x, y) received in 2 Sequence or np.ndarray of same length.
    ----------
    Parameters:
    ----
        x (Union[float, Sequence, np.ndarray]): Value(s) to be interpolated.
        known_xs (Union[Sequence, np.ndarray]): Sequence or np.ndarray of x values.
        known_ys (Union[Sequence, np.ndarray]): Sequence or np.ndarray of y values.
    ----
    Returns:
    ----
        result (Union[float, np.ndarray]): Interpolated y(x) value(s).
    '''
    log_known_ys = np.log(known_ys)
    log_y_result = linear_interpolation(x, known_xs, log_known_ys)
    result = np.exp(log_y_result)
    return result
    
def cubic_spline_interpolation(x, known_xs, known_ys):
    '''
    Cubic spline interpolation. interpolates y(x) for a given number of pairs (x, y) received in 2 Sequence or np.ndarray of same length.
    ----------
    Parameters:
    ----
        x (Union[float, Sequence, np.ndarray]): Value(s) to be interpolated.
        known_xs (Union[Sequence, np.ndarray]): Sequence or np.ndarray of x values.
        known_ys (Union[Sequence, np.ndarray]): Sequence or np.ndarray of y values.
    ----
    Returns:
    ----
        result (Union[float, np.ndarray]): Interpolated y(x) value(s).
    '''
    cs = CubicSpline(known_xs, known_ys)
    result = cs(x)
    return result

_interpolation_methods_map = {
    InterpolationMethod.LINEAR: linear_interpolation, 
    InterpolationMethod.LOGLINEAR: loglinear_interpolation, 
    InterpolationMethod.CUBIC_SPLINE: cubic_spline_interpolation
}

def interpolate(x: Union[float, Sequence, np.ndarray], known_xs: Union[Sequence, np.ndarray], known_ys: Union[Sequence, np.ndarray], interpolation_method: InterpolationMethod=InterpolationMethod.LINEAR) -> Union[float, np.ndarray]:
    '''
    Interpolates y(x) in a given number of pairs (x, y) received in 2 Sequence or np.ndarray of same length.    
    ----------
    Parameters:
    ----
        x (Union[float, Sequence, np.ndarray]): Value(s) to be interpolated.
        known_xs (Union[Sequence, np.ndarray]): Sequence or np.ndarray of x values.
        known_ys (Union[Sequence, np.ndarray]): Sequence or np.ndarray of y values.
        interpolation_method (InterpolationMethod): Optional. Interpolation method. Default is linear interpolation.
    ----
    Returns:
    ----
        Union[float, np.ndarray]
            Interpolated y(x) value(s).
    '''
    check_pairs_interpolation(known_xs, known_ys)
    interpolation_func = _interpolation_methods_map[interpolation_method]
    result = interpolation_func(x, known_xs, known_ys)
    result = adapt_interpolation_result(x, result)
    return result
