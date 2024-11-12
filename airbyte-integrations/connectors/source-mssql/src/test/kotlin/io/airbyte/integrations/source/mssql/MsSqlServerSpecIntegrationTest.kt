/*
 * Copyright (c) 2024 Airbyte, Inc., all rights reserved.
 */

package io.airbyte.integrations.source.mssql

import io.airbyte.cdk.command.SyncsTestFixture
import org.junit.jupiter.api.Test

class MsSqlServerSpecIntegrationTest {
    @Test
    fun testSpec() {
        SyncsTestFixture.testSpec("expected_spec.json")
    }
}
