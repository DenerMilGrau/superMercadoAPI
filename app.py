# importar biblioteca
from flask import Flask, jsonify, render_template, redirect, url_for
# importe para documentacao
from flask_pydantic_spec import FlaskPydanticSpec
from datetime import date
from dateutil.relativedelta import relativedelta

# [flask routes] para listar rotas da api

# criar variavel para receber a classe Flask
app = Flask(__name__)

#   documentacao OpenAPI
spec = FlaskPydanticSpec('flask',
                         title='First API - SENAI',
                         version='1.0.0')
spec.register(app)


@app.route('/')
def index():
    return redirect(url_for('verificar'))

@app.route('/verificar-validade')
@app.route('/verificar-validade/<tipo>/<valor>', methods=['GET', 'POST'])
def verificar(tipo=None, valor=None):

    """
        Api para calcular a data de validade com base no valor inserido, formato e data atual

        ### Endpoint:
            GET /verificar-validade

        ### Parâmetros:
        - `tipo`: tipo de data (semana, mes, dia)
        - `valor`: valor do tipo

        ### Resposta (JSON):
        ```json
        {
            "data_atual": 27/03/2025,
            "valor": 5,
            "tipo": "d",
            "data_validade": 01/04/2025
        }
        ```

        ## Erros Possíveis
        - Se `tipo` não for inserido corretamente ['d', 'w'...], retorna erro **400 Bad Request**
        - Se `valor` não for inserido corretamente (uma letra, por exemplo), retorna erro **400 Bad Request**

    """

    if tipo is None and valor is None:
        return jsonify({"error":"insira valores"
                        }), 400
    else:
        data_atual = date.today()
        tipos_validos = ['d', 'w', 'm','y']
        try:
            if tipo in tipos_validos:
                valor = int(valor)
                data_validade = data_atual
                if tipo == 'd':
                    data_validade = data_atual + relativedelta(days=valor)

                elif tipo == 'w':
                    data_validade = data_atual + relativedelta(weeks=valor)

                elif tipo == 'm':
                    data_validade = data_atual + relativedelta(months=valor)

                elif tipo == 'y':
                    data_validade = data_atual + relativedelta(years=valor)
                data_atual = data_atual.strftime('%d/%m/%Y')
                data_validade = data_validade.strftime('%d/%m/%Y')
                return jsonify({'data_atual': data_atual, 'valor': valor, 'data_validade': data_validade})
            else:
                raise TypeError
        except TypeError:
            return jsonify({'error': 'Erro de formato de data inserido'}), 400
        except ValueError:
            return jsonify({'error': 'Erro de valor inserido'}), 400


# iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)