import { describe, expect, it } from "vitest";
import { TestDriver } from "testdriverai/vitest/hooks";

describe("Sample Test Suite", () => {
  it("loads the application and verifies the interface", async (context) => {
    const testdriver = TestDriver(context);

    await testdriver.provision.chrome({ url: "https://demo.testdriver.ai" });

    const result = await testdriver.assert("the demo page is loaded");
    expect(result).toBeTruthy();
  });
});
