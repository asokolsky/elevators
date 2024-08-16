from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/attributes")
async def get_attributes():
    '''
    Present attributes
    '''
    return {
        "attr1": "foo",
        "attr2": 222,
        "attr3": {
            "baz": "bazz"
        },
        "attr4": [1, 2, 3]
    }

@app.get("/api/v1/indicators")
async def get_indicators():
    '''
    Present indicators
    '''
    return {
        "in1": "foo",
        "in2": 222,
    }
