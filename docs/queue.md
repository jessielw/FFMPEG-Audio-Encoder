# The encoding queue

Jobs run one at a time, in order. The queue is saved to disk as it changes, so closing the application does not lose it.

Toggle the panel with ++f9++.

## Job states

| State         | Meaning                                                  |
| ------------- | -------------------------------------------------------- |
| **Waiting**   | Queued, not yet dispatched                               |
| **Encoding**  | Currently running                                        |
| **Complete**  | Encoder exited successfully and the output was published |
| **Failed**    | Encoder failed, or the job could not be started          |
| **Cancelled** | You stopped it, or `Cancel all` dropped it before it ran |

A job whose encoder is no longer available - because you removed a tool, or moved to an FFmpeg build without it - shows **Unavailable encoder** instead of running.

## The toolbar

The toolbar is grouped by what the actions do.

**Queueing**

| Action                    | Effect                                          |
| ------------------------- | ----------------------------------------------- |
| **Queue selected inputs** | Add the selected inputs without starting them   |
| **Queue and start**       | Add them and begin immediately (++ctrl+enter++) |

**Running**

| Action | Effect |
| --- | --- |
| **Start queue** | Run every queued job in order |
| **Start selected** | Run only the selected queued jobs, and stop when they are done |

**Halting**

| Action | Effect |
| --- | --- |
| **Stop after current** | Let the running job finish, then hold the rest |
| **Cancel active** | Abort the running job. **The queue carries on with the next one.** |
| **Cancel all** | Abort the running job and mark everything queued as cancelled |

!!! warning "Cancel active does not stop the queue"

    It aborts one job. If you want everything to stop, use **Stop after current** or
    **Cancel all**.

**Housekeeping**

| Action | Effect |
| --- | --- |
| **Retry selected** | Requeue finished, failed, or cancelled jobs |
| **Remove selected** | Drop jobs from the queue. A running job is never removed. |
| **Clear finished** | Remove every succeeded, failed, and cancelled job |

## Retry

Retry accepts jobs in any terminal state - including **Complete**, so you can re-run something you deleted the output of.

The destination is re-validated first. If the output path has since become invalid - say another queued job now targets the same file - the job stays where it is and the reason appears in its error field rather than failing later.

## What survives a restart

The queue is written to a versioned `jobs.json` in the configuration directory, atomically: a temporary file is written and then renamed into place, so an interrupted write cannot truncate the real file.

On the next start:

- **Queued jobs stay queued, and stay paused.** Nothing resumes on its own. You decide when encoding starts again.
- **A job that was running is restored as Failed**, with the error _Application exited while this job was encoding_, and its partial `.part` file is deleted. That is deliberate - the application cannot know whether that encode was sound, so it hands it back for you to look at and retry rather than silently resuming or silently calling it done.
- Succeeded, failed, and cancelled jobs are restored as they were.

If `jobs.json` is corrupt, it is renamed to `<name>.corrupt-<timestamp>.<ext>` and the queue starts empty, rather than being overwritten. See [Files and locations](files.md).

## How outputs are protected

**Every encode writes to a job-specific `.part` file** next to the destination, and the file is renamed into place only after the encoder exits successfully. A crash, a cancellation, or a failed encode leaves the `.part` file, never a truncated file wearing the real name.

Two destinations are rejected before a job is queued:

- **An output that is the input.** You cannot encode a file over itself.
- **A destination another active job already targets.** Two queued jobs cannot race for the same path.

Generated names that collide with an existing file are numbered automatically, unless you tick **Replace an existing file** on the **Output** tab.

## Progress and logs

Progress comes from the encoder itself: FFmpeg's progress output for the built-in and standalone adapters, and DeeZy's numbered stage percentages for the Dolby ones - so a DeeZy job's bar reflects its measurement and encode stages rather than jumping from 0 to 100.

- **Selected job** shows the command that ran and any error.
- **Session log** holds the running output, bounded to the most recent 3,000 lines so a long session cannot grow without limit.

The right-click menu on a job offers **Start selected**, **Retry selected**, **Open output folder**, **Copy command**, **Copy error**, and **Remove selected**.

## On exit

Closing the application terminates every encoder process tree outright - including the grandchildren DeeZy spawns. See [DeeZy encoders](encoders/deezy.md#process-containment) for why that matters.
