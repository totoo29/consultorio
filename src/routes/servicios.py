from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from src.models import Servicio, Categoria
from src.services.servicio_service import ServicioService
from src.services.categoria_service import CategoriaService
from src.database import db

servicios_bp = Blueprint('servicios', __name__)

@servicios_bp.route('/')
def listar():
    """Listar todos los servicios"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '', type=str)
    categoria_id = request.args.get('categoria_id', type=int)
    
    servicios = ServicioService.get_paginated_servicios(page, per_page, search, categoria_id)
    categorias = CategoriaService.get_all_categorias()
    
    return render_template('servicios/listar.html', 
                         servicios=servicios, 
                         categorias=categorias,
                         search=search,
                         categoria_id=categoria_id)

@servicios_bp.route('/nuevo')
def nuevo():
    """Formulario para crear nuevo servicio"""
    categorias = CategoriaService.get_all_categorias()
    return render_template('servicios/formulario.html', categorias=categorias)

@servicios_bp.route('/crear', methods=['POST'])
def crear():
    """Crear nuevo servicio"""
    try:
        data = request.get_json() if request.is_json else request.form
        servicio = ServicioService.crear_servicio(data)
        
        if request.is_json:
            return jsonify({'success': True, 'servicio': servicio.to_dict()})
        
        flash('Servicio creado exitosamente', 'success')
        return redirect(url_for('servicios.listar'))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        
        flash(f'Error al crear servicio: {str(e)}', 'error')
        return redirect(url_for('servicios.nuevo'))

@servicios_bp.route('/<int:id>')
def detalle(id):
    """Ver detalle de un servicio"""
    servicio = ServicioService.get_servicio_by_id(id)
    if not servicio:
        flash('Servicio no encontrado', 'error')
        return redirect(url_for('servicios.listar'))
    
    return render_template('servicios/detalle.html', servicio=servicio)

@servicios_bp.route('/<int:id>/editar')
def editar(id):
    """Formulario para editar servicio"""
    servicio = ServicioService.get_servicio_by_id(id)
    if not servicio:
        flash('Servicio no encontrado', 'error')
        return redirect(url_for('servicios.listar'))
    
    categorias = CategoriaService.get_all_categorias()
    return render_template('servicios/formulario.html', 
                         servicio=servicio, 
                         categorias=categorias)

@servicios_bp.route('/<int:id>/actualizar', methods=['POST', 'PUT'])
def actualizar(id):
    """Actualizar servicio existente"""
    try:
        data = request.get_json() if request.is_json else request.form
        servicio = ServicioService.actualizar_servicio(id, data)
        
        if not servicio:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Servicio no encontrado'}), 404
            flash('Servicio no encontrado', 'error')
            return redirect(url_for('servicios.listar'))
        
        if request.is_json:
            return jsonify({'success': True, 'servicio': servicio.to_dict()})
        
        flash('Servicio actualizado exitosamente', 'success')
        return redirect(url_for('servicios.detalle', id=id))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        
        flash(f'Error al actualizar servicio: {str(e)}', 'error')
        return redirect(url_for('servicios.editar', id=id))

@servicios_bp.route('/<int:id>/eliminar', methods=['POST', 'DELETE'])
def eliminar(id):
    """Eliminar servicio"""
    try:
        success = ServicioService.eliminar_servicio(id)
        
        if not success:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Servicio no encontrado'}), 404
            flash('Servicio no encontrado', 'error')
            return redirect(url_for('servicios.listar'))
        
        if request.is_json:
            return jsonify({'success': True})
        
        flash('Servicio eliminado exitosamente', 'success')
        return redirect(url_for('servicios.listar'))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        
        flash(f'Error al eliminar servicio: {str(e)}', 'error')
        return redirect(url_for('servicios.listar'))

@servicios_bp.route('/buscar')
def buscar():
    """API para buscar servicios"""
    query = request.args.get('q', '')
    categoria_id = request.args.get('categoria_id', type=int)
    limit = request.args.get('limit', 10, type=int)
    
    servicios = ServicioService.buscar_servicios(query, categoria_id, limit)
    
    return jsonify([servicio.to_dict() for servicio in servicios])

@servicios_bp.route('/api/todos')
def api_todos():
    """API para obtener todos los servicios activos"""
    categoria_id = request.args.get('categoria_id', type=int)
    servicios = ServicioService.get_all_servicios(categoria_id)
    return jsonify([servicio.to_dict() for servicio in servicios])

@servicios_bp.route('/por-categoria/<int:categoria_id>')
def por_categoria(categoria_id):
    """Listar servicios por categoría"""
    categoria = CategoriaService.get_categoria_by_id(categoria_id)
    if not categoria:
        flash('Categoría no encontrada', 'error')
        return redirect(url_for('servicios.listar'))
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '', type=str)
    
    servicios = ServicioService.get_paginated_servicios(page, per_page, search, categoria_id)
    
    return render_template('servicios/listar.html', 
                         servicios=servicios,
                         categoria=categoria,
                         search=search)