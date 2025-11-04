#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test module for auto-generating ToDo from stage tasks.

This module tests the new functionality that automatically creates
ToDo items based on the tasks defined in stage configurations.
"""

import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)

from vagent.tools.planning import ToDoPanel
from vagent.stage.vmanager import StageManager
from vagent.util.config import Config


class TestAutoCreateToDoFromStage(unittest.TestCase):
    """Test auto-generation of ToDo from stage tasks."""

    def setUp(self):
        """Set up test fixtures."""
        self.todo_panel = ToDoPanel()
        
    def test_auto_create_todo_basic(self):
        """Test basic auto-creation of ToDo from stage tasks."""
        # Mock a stage with tasks
        mock_stage = MagicMock()
        mock_stage.name = "test_stage"
        mock_stage.description.return_value = "Test Stage Description"
        mock_stage.task.return_value = [
            "Task 1: Do something",
            "Task 2: Do something else",
            "Task 3: Complete the work"
        ]
        
        # Mock StageManager
        mock_manager = MagicMock()
        mock_manager.todo_panel = self.todo_panel
        mock_manager.stage_index = 0
        mock_manager.stages = [mock_stage]
        
        # Call the method we're testing
        result = StageManager.auto_create_todo_from_stage(mock_manager, stage_index=0)
        
        # Verify ToDo was created
        self.assertIn("ToDo created successfully", result)
        self.assertFalse(self.todo_panel._empty())
        self.assertEqual(len(self.todo_panel.todo_list['steps']), 3)
        
    def test_auto_create_todo_no_panel(self):
        """Test auto-creation when todo_panel is not initialized."""
        mock_stage = MagicMock()
        mock_stage.task.return_value = ["Task 1", "Task 2"]
        
        mock_manager = MagicMock()
        mock_manager.todo_panel = None
        mock_manager.stages = [mock_stage]
        
        result = StageManager.auto_create_todo_from_stage(mock_manager, stage_index=0)
        
        self.assertIn("ToDo panel is not initialized", result)
        
    def test_auto_create_todo_empty_tasks(self):
        """Test auto-creation when stage has no tasks."""
        mock_stage = MagicMock()
        mock_stage.name = "empty_stage"
        mock_stage.task.return_value = []
        
        mock_manager = MagicMock()
        mock_manager.todo_panel = self.todo_panel
        mock_manager.stages = [mock_stage]
        
        result = StageManager.auto_create_todo_from_stage(mock_manager, stage_index=0)
        
        self.assertIn("has no tasks defined", result)
        
    def test_auto_create_todo_invalid_index(self):
        """Test auto-creation with invalid stage index."""
        mock_manager = MagicMock()
        mock_manager.todo_panel = self.todo_panel
        mock_manager.stages = []
        
        result = StageManager.auto_create_todo_from_stage(mock_manager, stage_index=5)
        
        self.assertIn("Invalid stage index", result)
    
    def test_auto_create_todo_negative_index(self):
        """Test auto-creation with negative stage index."""
        mock_stage = MagicMock()
        mock_stage.task.return_value = ["Task 1"]
        
        mock_manager = MagicMock()
        mock_manager.todo_panel = self.todo_panel
        mock_manager.stages = [mock_stage]
        
        result = StageManager.auto_create_todo_from_stage(mock_manager, stage_index=-1)
        
        self.assertIn("Invalid stage index", result)
        
    def test_auto_create_todo_uses_current_stage(self):
        """Test that auto-creation uses current stage when no index provided."""
        mock_stage1 = MagicMock()
        mock_stage1.name = "requirement_analysis"
        mock_stage1.description.return_value = "Requirement Analysis"
        mock_stage1.task.return_value = ["Task A"]
        
        mock_stage2 = MagicMock()
        mock_stage2.name = "implementation"
        mock_stage2.description.return_value = "Implementation Phase"
        mock_stage2.task.return_value = ["Task B", "Task C"]
        
        mock_manager = MagicMock()
        mock_manager.todo_panel = self.todo_panel
        mock_manager.stage_index = 1  # Current stage is index 1
        mock_manager.stages = [mock_stage1, mock_stage2]
        
        result = StageManager.auto_create_todo_from_stage(mock_manager, stage_index=None)
        
        # Should create ToDo from stage2 (index 1)
        self.assertIn("ToDo created successfully", result)
        self.assertEqual(len(self.todo_panel.todo_list['steps']), 2)
        self.assertIn("Stage 1: Implementation Phase", self.todo_panel.todo_list['task_description'])


if __name__ == '__main__':
    unittest.main()
