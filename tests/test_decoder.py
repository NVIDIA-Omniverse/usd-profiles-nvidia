# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import json
import unittest

from nvidia_usd_profiles.model import (
    Capability,
    Compatibility,
    Example,
    ExampleResult,
    ExampleSnippet,
    ExampleSnippetLanguage,
    Feature,
    IdVersion,
    Metadata,
    Parameter,
    ParameterType,
    Profile,
    Requirement,
    Tag,
    Version,
)
from nvidia_usd_profiles.serialization import (
    JsonDeserialize,
)


class TestJsonDeserialization(unittest.TestCase):
    """Test cases for JsonDeserialize JSON decoder."""

    def setUp(self):
        """Set up test fixtures."""
        self.decoder = JsonDeserialize()

    def test_deserialize_capability(self):
        """Test deserialization of Capability objects."""
        json_data = {
            "capability": {
                "id": "test_capability",
                "version": "1.0.0",
                "name": "Test Capability",
                "description": "A test capability",
                "requirements": [],
                "metadata": {"path": "test/capability.html"},
            }
        }

        result = json.loads(json.dumps(json_data), cls=JsonDeserialize)

        self.assertIsInstance(result, Capability)
        self.assertEqual(result.id, "test_capability")
        self.assertEqual(result.version, Version(1, 0, 0))
        self.assertEqual(result.name, "Test Capability")
        self.assertEqual(result.description, "A test capability")
        self.assertEqual(result.requirements, [])
        self.assertIsInstance(result.metadata, Metadata)

    def test_deserialize_profile(self):
        """Test deserialization of Profile objects."""
        json_data = {
            "profile": {
                "id": "test_profile",
                "version": "1.0.0",
                "name": "Test Profile",
                "description": "A test profile",
                "features": [],
                "metadata": {"path": "test/profile.html"},
            }
        }

        result = json.loads(json.dumps(json_data), cls=JsonDeserialize)

        self.assertIsInstance(result, Profile)
        self.assertEqual(result.id, "test_profile")
        self.assertEqual(result.version, Version(1, 0, 0))
        self.assertEqual(result.name, "Test Profile")
        self.assertEqual(result.description, "A test profile")
        self.assertEqual(result.features, [])

    def test_deserialize_feature(self):
        """Test deserialization of Feature objects."""
        json_data = {
            "feature": {
                "id": "test_feature",
                "version": "1.0.0",
                "name": "Test Feature",
                "description": "A test feature",
                "requirements": ["REQ_001@1.0.0", "REQ_002"],
                "metadata": {"path": "test/feature.html"},
            }
        }

        result = json.loads(json.dumps(json_data), cls=JsonDeserialize)

        self.assertIsInstance(result, Feature)
        self.assertEqual(result.id, "test_feature")
        self.assertEqual(result.version, Version(1, 0, 0))
        self.assertEqual(result.name, "Test Feature")
        self.assertEqual(result.description, "A test feature")
        self.assertEqual(result.requirements, [IdVersion.parse("REQ_001@1.0.0"), IdVersion.parse("REQ_002")])

    def test_deserialize_requirement(self):
        """Test deserialization of Requirement objects."""
        json_data = {
            "code": "TEST_REQ_001",
            "version": "1.0.0",
            "name": "Test Requirement",
            "compatibility": "openusd",
            "tags": "performance",
            "metadata": {"path": "test/requirement.html"},
            "message": "A test requirement",
        }

        result = json.loads(json.dumps(json_data), cls=JsonDeserialize)

        self.assertIsInstance(result, Requirement)
        self.assertEqual(result.code, "TEST_REQ_001")
        self.assertEqual(result.version, Version(1, 0, 0))
        self.assertEqual(result.name, "Test Requirement")
        self.assertEqual(result.compatibility, Compatibility.OPENUSD)
        self.assertEqual(result.tags, Tag.PERFORMANCE)
        self.assertEqual(result.description, "A test requirement")
        self.assertIsInstance(result.metadata, Metadata)

    def test_deserialize_metadata(self):
        """Test deserialization of Metadata objects."""
        json_data = {"path": "test/metadata.html"}

        result = json.loads(json.dumps(json_data), cls=JsonDeserialize)

        self.assertIsInstance(result, Metadata)

    def test_deserialize_example(self):
        """Test deserialization of Example objects."""
        json_data = {
            "snippet": {"language": "python", "content": "print('Hello, World!')"},
            "name": "A test example",
            "result": "success",
        }

        result = json.loads(json.dumps(json_data), cls=JsonDeserialize)

        self.assertIsInstance(result, Example)
        self.assertEqual(result.snippet.language, ExampleSnippetLanguage.PYTHON)
        self.assertEqual(result.snippet.content, "print('Hello, World!')")
        self.assertEqual(result.name, "A test example")
        self.assertEqual(result.result, ExampleResult.SUCCESS)

    def test_deserialize_example_snippet(self):
        """Test deserialization of ExampleSnippet objects."""
        json_data = {"language": "usd", "content": "def Xform 'Root' {}"}

        result = json.loads(json.dumps(json_data), cls=JsonDeserialize)

        self.assertIsInstance(result, ExampleSnippet)
        self.assertEqual(result.language, ExampleSnippetLanguage.USD)
        self.assertEqual(result.content, "def Xform 'Root' {}")

    def test_deserialize_parameter(self):
        """Test deserialization of Parameter objects."""
        json_data = {
            "display_name": "UP_AXIS",
            "type": "enum",
            "assigned_value": "Y",
            "enum_values": ["X", "Y", "Z"],
        }

        result = json.loads(json.dumps(json_data), cls=JsonDeserialize)

        self.assertIsInstance(result, Parameter)
        self.assertEqual(result.display_name, "UP_AXIS")
        self.assertEqual(result.type, ParameterType.ENUM)
        self.assertEqual(result.assigned_value, "Y")
        self.assertEqual(result.enum_values, ["X", "Y", "Z"])
