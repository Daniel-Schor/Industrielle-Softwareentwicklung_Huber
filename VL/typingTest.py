from typing import Optional


def division(
        x: float, 
        y: float
) -> Optional[float]:
    """
        Funktion zur Division von zwei Zahlen
    
    :param x: erster
    :param y: zweiter 
    :return: Ergebnis der Division  
    """

    result = None

    try:
        result: Optional[float] =  x / y
    except ZeroDivisionError:
        print("Division durch 0 nicht möglich")
    else:
        print(f"Das ergebnis lautet: {result}")
    finally:
        return result
    
if __name__ == "__main__":
    division(10, 2)
    division(10, 0)
    division(10, 5)
    division(10, 3)