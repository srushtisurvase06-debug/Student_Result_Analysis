from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os
import logging
from config import config


# Load environment variables
load_dotenv()


def create_app():
    """Application factory function for Flask app"""
    app = Flask(__name__)
    
    # Load configuration based on environment
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    
    # Configure logging
    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        app.logger.setLevel(logging.INFO)
        
        # Add console handler for production
        import sys
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning(f'404 Not Found: {error}')
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal error: {error}')
        return render_template('errors/500.html'), 500
    
    # Register blueprints (to be implemented in future phases)
    # from routes import auth, dashboard, students, subjects, marks, results, analysis, reports
    # app.register_blueprint(auth.bp)
    # app.register_blueprint(dashboard.bp)
    # app.register_blueprint(students.bp)
    # app.register_blueprint(subjects.bp)
    # app.register_blueprint(marks.bp)
    # app.register_blueprint(results.bp)
    # app.register_blueprint(analysis.bp)
    # app.register_blueprint(reports.bp)
    
    # Test routes
    @app.route('/')
    def index():
        """Root endpoint - API status"""
        return jsonify({
            'message': 'Student Result Analysis System API',
            'version': '1.0',
            'status': 'running'
        })
    
    @app.route('/health')
    def health():
        """Health check endpoint for deployment monitoring"""
        return jsonify({'status': 'healthy'}), 200
    
    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
