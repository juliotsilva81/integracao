from flask import Blueprint, jsonify, request

event = Blueprint('event', __name__)

@event.route('/device_is_alive.fcgi', methods=['POST'])
def device_is_alive():
    print('event.device_is_alive')
    print(request.get_json())
    print(request.args)

    return jsonify(
        access_logs=request.get_json()['access_logs']
    )

@event.route('/create_student.fcgi', methods=['POST'])
def create_student():
    data = request.get_json()
    print(data)
    
    # Criar um novo aluno no banco de dados
    new_student = Aluno(nome=data.get('nome'), email=data.get('email'))
    db.session.add(new_student)
    db.session.commit()

    return jsonify(
        message="Aluno criado com sucesso"
    )

@event.route('/list_students.fcgi', methods=['GET'])
def list_students():
    students = Aluno.query.all()
    return jsonify([{'id': student.id, 'nome': student.nome, 'email': student.email} for student in students])

@event.route('/update_student.fcgi/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    student = Aluno.query.get(id)
    if student:
        student.nome = data.get('nome', student.nome)
        student.email = data.get('email', student.email)
        db.session.commit()
        return jsonify(message="Aluno atualizado com sucesso")
    return jsonify(message="Aluno não encontrado"), 404

@event.route('/delete_student.fcgi/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Aluno.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify(message="Aluno excluído com sucesso")
    return jsonify(message="Aluno não encontrado"), 404
