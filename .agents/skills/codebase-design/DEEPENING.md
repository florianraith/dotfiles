# Deepening

How to deepen a cluster of shallow modules safely, given its dependencies. Assumes the vocabulary in [SKILL.md](SKILL.md) — **module**, **interface**, **seam**, **adapter**.

## Dependency categories

When assessing a candidate for deepening, classify its dependencies. The category determines how the deepened module is tested across its seam.

### 1. In-process

Pure computation, in-memory state, no I/O. Always deepenable — merge the modules and test through the new interface directly. No adapter needed.

### 2. Local-substitutable

Dependencies the test suite can run for real, cheaply. The usual case is the database: the real engine in a container against a dedicated test schema, with `RefreshDatabase` per test file. `Storage::fake()` covers the filesystem the same way. SQLite `:memory:` is the lighter alternative when the suite doesn't depend on engine-specific behaviour.

Deepenable whenever the substitute exists. The deepened module is tested against it directly. The seam is internal; no port at the module's external interface.

### 3. Remote but owned (Ports & Adapters)

Your own services across a network boundary (internal APIs, queued work handled elsewhere). Define a **port** (interface) at the seam. The deep module owns the logic; the transport is injected as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP or queue adapter.

Mechanically, in Laravel: declare the interface, type the constructor or method parameter against it, and choose the adapter at the call site. Reach for a service-provider binding (`bind()`, `singleton()`, contextual binding) only when the adapter must be chosen globally rather than per call.

Recommendation shape: *"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it's deployed across a network."*

### 4. True external (Mock)

Third-party services you don't control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

**Unless it fakes itself.** Many packages ship their own test seam — the HTTP client via `Http::fake()`, or a per-class static fake (`SomeAgent::fake([...])`) as some SDKs offer. When the dependency already offers one, use it; wrapping it in a port of your own buys nothing. Inject a port only for third parties with no fake of their own.

## Seam discipline

- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a port unless at least two adapters are justified (typically production + test). A single-adapter seam is just indirection. Two real implementations chosen per call pass this test without any container involvement.
- **Framework fakes are a seam you didn't design — use it.** `Storage::fake()`, `Http::fake()`, `Queue::fake()`, `Notification::fake()`, and self-faking SDK classes already give you the substitution a port would have given you. Define your own port only for dependencies Laravel and its packages don't fake. Wrapping a fakeable facade in a bespoke interface is the single-adapter mistake in Laravel dress.
- **Internal seams vs external seams.** A deep module can have internal seams (private to its implementation, used by its own tests) as well as the external seam at its interface. Don't expose internal seams through the interface just because tests use them.

## Testing strategy: replace, don't layer

- Old unit tests on shallow modules become waste once tests at the deepened module's interface exist — delete them.
- Write new tests at the deepened module's interface. The **interface is the test surface**.
- Tests assert on observable outcomes through the interface, not internal state.
- Tests should survive internal refactors — they describe behaviour, not implementation. If a test has to change when the implementation changes, it's testing past the interface.
