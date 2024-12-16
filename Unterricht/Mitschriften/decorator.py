def convert(data_type: type):
    def decorator(function):

        def wrapper(*args, **kwargs):

            result = function(*args, **kwargs)

            print(f'Konvertiere von: {type(result)} nach {data_type}. \n Ergebnis: {data_type(result)}')

            return data_type(result)

        return wrapper
    
    return decorator


@convert(float)
def add(a, b):
    return a + b


if __name__ == '__main__':
    add(1, 2)