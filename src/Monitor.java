import oshi.SystemInfo;
import oshi.hardware.CentralProcessor;
import oshi.software.os.OperatingSystem;
import oshi.software.os.OSProcess;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;

import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Map;
import java.util.stream.Collectors;

public class Monitor {
    public static void main(String[] args) {
        SystemInfo si = new SystemInfo();
        CentralProcessor cpu = si.getHardware().getProcessor();
        OperatingSystem os = si.getOperatingSystem();
        ObjectMapper mapper = new ObjectMapper();

        int intervalMs = Integer.parseInt(System.getenv().getOrDefault("MONITOR_INTERVAL_MS", "5000"));
        int maxHistorySize = Integer.parseInt(System.getenv().getOrDefault("METRIC_HISTORY_LIMIT", "500"));

        File metricsFile = new File("shared/metrics.json");
        metricsFile.getParentFile().mkdirs();

        while (true) {
            try {
                long[] prevTicks = cpu.getSystemCpuLoadTicks();
                Thread.sleep(intervalMs);
                long[] ticks = cpu.getSystemCpuLoadTicks();
                double cpuLoad = cpu.getSystemCpuLoadBetweenTicks(prevTicks) * 100;

                long totalMem = si.getHardware().getMemory().getTotal();
                long availMem = si.getHardware().getMemory().getAvailable();
                double memUsedPercent = (totalMem - availMem) * 100.0 / totalMem;

                int procCount = os.getProcessCount();

                // ✅ Fetch top process by CPU usage (compatible with OSHI 6.4.0)
                List<OSProcess> sortedProcs = os.getProcesses(
                        p -> true,
                        Comparator.comparing(OSProcess::getProcessCpuLoadCumulative).reversed(),
                        5);

                OSProcess topProc = sortedProcs.isEmpty() ? null : sortedProcs.get(0);
                String topProcName = topProc != null ? topProc.getName() : "Unknown";

                Map<String, Object> metrics = new HashMap<>();
                metrics.put("timestamp", System.currentTimeMillis());
                metrics.put("cpu", cpuLoad);
                metrics.put("mem", memUsedPercent);
                metrics.put("proc_count", procCount);
                metrics.put("top_proc", topProcName);

                List<Map<String, Object>> history;
                if (metricsFile.exists()) {
                    try {
                        history = mapper.readValue(
                                metricsFile,
                                new TypeReference<List<Map<String, Object>>>() {
                                });
                    } catch (Exception e) {
                        System.err.println("❗ Error reading JSON history: " + e.getMessage());
                        history = new ArrayList<>();
                    }
                } else {
                    history = new ArrayList<>();
                }

                history.add(metrics);
                if (history.size() > maxHistorySize) {
                    history.remove(0); // drop oldest to keep JSON lean
                }

                mapper.writeValue(metricsFile, history);

            } catch (InterruptedException ie) {
                System.err.println("⚠ Monitor interrupted");
                Thread.currentThread().interrupt();
                break;
            } catch (Exception e) {
                System.err.println("❗ Monitor error: " + e.getMessage());
                break;
            }
        }
    }
}