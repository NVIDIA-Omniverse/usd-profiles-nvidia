# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import json
import unittest

from nvidia_usd_profiles.model import (
    Capability,
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
    Version,
)
from nvidia_usd_profiles.serialization import (
    JsonDeserialize,
    JsonSerialize,
)


class TestJsonSerialization(unittest.TestCase):
    """Test cases for JsonSerialize JSON encoder."""

    def setUp(self):
        """Set up test fixtures."""
        self.encoder = JsonSerialize()
        self.decoder = JsonDeserialize()

    def test_serialize_requirement(self):
        """Test serialization of Requirement objects."""
        metadata = Metadata("capabilities/test-requirement.md")
        requirement = Requirement(
            code="TEST_REQ_001",
            version=Version(1, 0, 0),
            name="Test Requirement",
            description="A test requirement for unit testing",
            compatibility="high",
            tags="test,unit",
            metadata=metadata,
        )

        result = json.loads(json.dumps(requirement, cls=JsonSerialize))

        expected = {
            "code": "TEST_REQ_001",
            "version": "1.0.0",
            "name": "Test Requirement",
            "compatibility": "high",
            "tags": "test,unit",
            "validator": None,
            "parameters": [],
            "metadata": {
                "path": "capabilities/test-requirement.html",
                "internal_path": "capabilities/test-requirement.md",
            },
            "message": "A test requirement for unit testing",
            "examples": [],
        }

        self.assertEqual(result, expected)

    def test_serialize_requirement_with_none_values(self):
        """Test serialization of Requirement with None values."""
        requirement = Requirement(code="TEST_REQ_002", name="Test Requirement 2")

        result = json.loads(json.dumps(requirement, cls=JsonSerialize))

        expected = {
            "code": "TEST_REQ_002",
            "version": None,
            "name": "Test Requirement 2",
            "compatibility": None,
            "tags": None,
            "validator": None,
            "parameters": [],
            "metadata": {"path": ".html", "internal_path": ".md"},
            "message": None,
            "examples": [],
        }

        self.assertEqual(result, expected)

    def test_serialize_capability(self):
        """Test serialization of Capability objects."""
        metadata = Metadata("capabilities/test-capability.md")
        requirement = Requirement(code="REQ_001", name="Test Req")

        capability = Capability(
            id="test_capability",
            version=Version(1, 0, 0),
            name="Test Capability",
            description="A test capability",
            requirements=[requirement],
            metadata=metadata,
        )

        result = json.loads(json.dumps(capability, cls=JsonSerialize))

        self.assertIn("capability", result)
        cap_data = result["capability"]
        self.assertEqual(cap_data["id"], "test_capability")
        self.assertEqual(cap_data["version"], "1.0.0")
        self.assertEqual(cap_data["name"], "Test Capability")
        self.assertEqual(cap_data["description"], "A test capability")
        self.assertEqual(len(cap_data["requirements"]), 1)
        self.assertIn("metadata", cap_data)

    def test_serialize_profile(self):
        """Test serialization of Profile objects."""
        metadata = Metadata("profiles/test-profile.md")

        profile = Profile(
            id="test_profile",
            version=Version(1, 0, 0),
            name="Test Profile",
            description="A test profile",
            metadata=metadata,
            features=[IdVersion("test_feature", Version(1, 0, 0))],
        )

        result = json.loads(json.dumps(profile, cls=JsonSerialize))

        self.assertIn("profile", result)
        prof_data = result["profile"]
        self.assertEqual(prof_data["id"], "test_profile")
        self.assertEqual(prof_data["version"], "1.0.0")
        self.assertEqual(prof_data["name"], "Test Profile")
        self.assertEqual(prof_data["description"], "A test profile")
        self.assertEqual(len(prof_data["features"]), 1)

    def test_serialize_feature(self):
        """Test serialization of Feature objects."""
        metadata = Metadata("features/test-feature.md")

        feature = Feature(
            id="test_feature",
            version=Version(1, 0, 0),
            name="Test Feature",
            description="A test feature",
            requirements=[IdVersion("FEAT_REQ_001")],
            metadata=metadata,
        )

        result = json.loads(json.dumps(feature, cls=JsonSerialize))

        self.assertIn("feature", result)
        feat_data = result["feature"]
        self.assertEqual(feat_data["id"], "test_feature")
        self.assertEqual(feat_data["version"], "1.0.0")
        self.assertEqual(feat_data["name"], "Test Feature")
        self.assertEqual(feat_data["description"], "A test feature")
        self.assertEqual(len(feat_data["requirements"]), 1)

    def test_serialize_metadata(self):
        """Test serialization of Metadata objects."""
        metadata = Metadata("test/example.md")

        result = json.loads(json.dumps(metadata, cls=JsonSerialize))

        expected = {"path": "test/example.html", "internal_path": "test/example.md"}

        self.assertEqual(result, expected)

    def test_serialize_parameter(self):
        """Test serialization of Parameter objects."""
        param = Parameter(display_name="AXIS", type=ParameterType.ENUM, assigned_value="X", enum_values=["X", "Y", "Z"])
        result = json.loads(json.dumps(param, cls=JsonSerialize))

        expected = {
            "display_name": "AXIS",
            "type": "enum",
            "assigned_value": "X",
            "enum_values": ["X", "Y", "Z"],
        }

        self.assertEqual(result, expected)

    def test_serialize_example(self):
        """Test serialization of Example objects."""
        example = Example(
            snippet=ExampleSnippet(language=ExampleSnippetLanguage.PYTHON, content="print('Hello, World!')"),
            name="A test example",
            result=ExampleResult.SUCCESS,
        )
        result = json.loads(json.dumps(example, cls=JsonSerialize))

        expected = {
            "snippet": {
                "language": "python",
                "content": "print('Hello, World!')",
            },
            "name": "A test example",
            "result": "success",
        }
        self.assertEqual(result, expected)

    def test_serialize_example_snippet(self):
        """Test serialization of ExampleSnippet objects."""
        snippet = ExampleSnippet(language=ExampleSnippetLanguage.USD, content="def Xform 'Root' {}")
        result = json.loads(json.dumps(snippet, cls=JsonSerialize))

        expected = {"language": "usd", "content": "def Xform 'Root' {}"}
        self.assertEqual(result, expected)

    def test_serialize_version(self):
        """Test serialization of Version objects."""
        version = Version(2, 5, 1)
        result = json.loads(json.dumps(version, cls=JsonSerialize))

        self.assertEqual(result, "2.5.1")

    def test_serialize_id_version(self):
        """Test serialization of IdVersion objects."""
        # With version
        id_version = IdVersion("REQ_001", Version(1, 0, 0))
        result = json.loads(json.dumps(id_version, cls=JsonSerialize))
        self.assertEqual(result, "REQ_001@1.0.0")

        # Without version
        id_version_no_ver = IdVersion("REQ_002", None)
        result_no_ver = json.loads(json.dumps(id_version_no_ver, cls=JsonSerialize))
        self.assertEqual(result_no_ver, "REQ_002")
