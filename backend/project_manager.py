"""
Project manager for saving and loading projects.
Uses SQLite database for local storage.
"""
import os
import sqlite3
import json
import shutil
from datetime import datetime
from typing import List, Dict, Optional
from image_manager import ImageManager


class ProjectManager:
    """Manages project storage and retrieval using SQLite."""
    
    def __init__(self, db_path: str = "projects.db"):
        """
        Initialize project manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Captures table (linked to projects)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS captures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                capture_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                click_x INTEGER NOT NULL,
                click_y INTEGER NOT NULL,
                window_title TEXT,
                url TEXT,
                context TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                UNIQUE(project_id, capture_id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_project_id ON captures(project_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_capture_id ON captures(capture_id)')
        
        conn.commit()
        conn.close()
    
    def create_project(self, name: str, description: str = "") -> int:
        """
        Create a new project.
        
        Args:
            name: Project name
            description: Project description
            
        Returns:
            Project ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO projects (name, description, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (name, description, now, now))
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return project_id
    
    def list_projects(self) -> List[Dict]:
        """
        List all projects.
        
        Returns:
            List of project dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, created_at, updated_at
            FROM projects
            ORDER BY updated_at DESC
        ''')
        
        projects = []
        for row in cursor.fetchall():
            projects.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'created_at': row[3],
                'updated_at': row[4]
            })
        
        conn.close()
        return projects
    
    def get_project(self, project_id: int) -> Optional[Dict]:
        """
        Get a project by ID.
        
        Args:
            project_id: Project ID
            
        Returns:
            Project dictionary or None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, created_at, updated_at
            FROM projects
            WHERE id = ?
        ''', (project_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'created_at': row[3],
                'updated_at': row[4]
            }
        return None
    
    def save_project(self, project_id: int, image_manager: ImageManager, captures_dir: str = "captures") -> bool:
        """
        Save current captures to a project.
        Copies image files to project-specific directory.
        
        Args:
            project_id: Project ID to save to
            image_manager: ImageManager instance with current captures
            captures_dir: Directory where capture images are stored
            
        Returns:
            True if successful
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all current captures
        captures = image_manager.get_all_captures()
        
        # Create project-specific directory for images
        project_dir = os.path.join(captures_dir, f"project_{project_id}")
        os.makedirs(project_dir, exist_ok=True)
        
        # Delete existing captures for this project
        cursor.execute('DELETE FROM captures WHERE project_id = ?', (project_id,))
        
        # Clear old project images
        if os.path.exists(project_dir):
            for file in os.listdir(project_dir):
                if file.endswith('.png'):
                    os.remove(os.path.join(project_dir, file))
        
        # Insert new captures and copy images
        for capture in captures:
            # Copy image file to project directory
            source_path = image_manager.get_image_path(capture['id'])
            if source_path and os.path.exists(source_path):
                dest_path = os.path.join(project_dir, capture['filename'])
                try:
                    shutil.copy2(source_path, dest_path)
                except Exception as e:
                    print(f"Warning: Failed to copy image {capture['filename']} to project: {e}")
            else:
                print(f"Warning: Source image not found for capture {capture['id']}: {source_path}")
            
            cursor.execute('''
                INSERT INTO captures 
                (project_id, capture_id, filename, timestamp, click_x, click_y, window_title, url, context)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                project_id,
                capture['id'],
                capture['filename'],
                capture['timestamp'],
                capture['click_x'],
                capture['click_y'],
                capture.get('window_title', ''),
                capture.get('url', ''),
                capture.get('context', '')
            ))
        
        # Update project timestamp
        cursor.execute('''
            UPDATE projects SET updated_at = ? WHERE id = ?
        ''', (datetime.now().isoformat(), project_id))
        
        conn.commit()
        conn.close()
        return True
    
    def load_project(self, project_id: int, image_manager: ImageManager, captures_dir: str = "captures") -> bool:
        """
        Load a project's captures into the current session.
        Restores metadata and copies image files back to main captures directory.
        
        Args:
            project_id: Project ID to load
            image_manager: ImageManager instance to load captures into
            captures_dir: Directory where capture images are stored
            
        Returns:
            True if successful
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all captures for this project
        cursor.execute('''
            SELECT capture_id, filename, timestamp, click_x, click_y, window_title, url, context
            FROM captures
            WHERE project_id = ?
            ORDER BY timestamp ASC
        ''', (project_id,))
        
        captures = cursor.fetchall()
        conn.close()
        
        if not captures:
            # No captures to load
            image_manager._save_metadata([])
            return True
        
        # Ensure captures directory exists
        os.makedirs(captures_dir, exist_ok=True)
        
        # Clear current captures directory (only .png files, not subdirectories)
        if os.path.exists(captures_dir):
            for file in os.listdir(captures_dir):
                file_path = os.path.join(captures_dir, file)
                # Only delete .png files, not directories
                if os.path.isfile(file_path) and file.endswith('.png'):
                    try:
                        os.remove(file_path)
                    except:
                        pass
        
        # Clear current metadata
        image_manager._save_metadata([])
        
        # Project directory
        project_dir = os.path.join(captures_dir, f"project_{project_id}")
        
        # Restore metadata and copy images
        restored_captures = []
        for row in captures:
            capture_data = {
                'id': row[0],
                'filename': row[1],
                'timestamp': row[2],
                'click_x': row[3],
                'click_y': row[4],
                'window_title': row[5] if row[5] else '',
                'url': row[6] if row[6] else '',
                'context': row[7] if row[7] else ''
            }
            
            # Copy image file from project directory to main captures directory
            source_path = os.path.join(project_dir, row[1])
            dest_path = os.path.join(captures_dir, row[1])
            
            if os.path.exists(source_path):
                try:
                    shutil.copy2(source_path, dest_path)
                except Exception as e:
                    print(f"Warning: Failed to copy image {row[1]}: {e}")
                    # Continue even if image copy fails
            else:
                print(f"Warning: Image file not found: {source_path}")
            
            restored_captures.append(capture_data)
        
        # Save restored metadata
        image_manager._save_metadata(restored_captures)
        
        return True
    
    def delete_project(self, project_id: int, captures_dir: str = "captures") -> bool:
        """
        Delete a project and all its captures.
        Also deletes the project's image directory.
        
        Args:
            project_id: Project ID to delete
            captures_dir: Directory where capture images are stored
            
        Returns:
            True if successful
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        # Captures are automatically deleted due to CASCADE
        
        conn.commit()
        conn.close()
        
        # Delete project image directory
        project_dir = os.path.join(captures_dir, f"project_{project_id}")
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        
        return True
    
    def update_project(self, project_id: int, name: str = None, description: str = None) -> bool:
        """
        Update project name or description.
        
        Args:
            project_id: Project ID
            name: New name (optional)
            description: New description (optional)
            
        Returns:
            True if successful
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if name is not None:
            updates.append('name = ?')
            params.append(name)
        
        if description is not None:
            updates.append('description = ?')
            params.append(description)
        
        if updates:
            updates.append('updated_at = ?')
            params.append(datetime.now().isoformat())
            params.append(project_id)
            
            cursor.execute(f'''
                UPDATE projects SET {', '.join(updates)} WHERE id = ?
            ''', params)
            
            conn.commit()
        
        conn.close()
        return True

