import org.apache.hadoop.conf.Configured;
import java.io.IOException;
import java.nio.file.AccessDeniedException;
import java.util.ArrayList;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import java.util.Iterator;
import org.apache.hadoop.conf.Configuration;
import java.util.Arrays;
import java.util.List;

public class QSevenReducer2 extends Reducer<Text, Text, Text, Text>  
{
    // private String targetid1 = "3577"; // a Seattle airport
    // private String targetid2 = "3797"; // a New York airport

    private List<String> targetid1; // a Seattle airport [should change to a list]
    private List<String> targetid2;

    public void setup(Context context)
    {
        Configuration conf = context.getConfiguration();
        targetid1 = Arrays.asList(conf.get("TargetId1").strip().split("\\s+"));
        targetid2 = Arrays.asList(conf.get("TargetId2").strip().split("\\s+"));
    }

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException
    {
        ArrayList<String> paths = new ArrayList<String>();
        ArrayList<String> adjacent = new ArrayList<String>();

        // check for valid paths
        String p;
        String[] path;
        for(Text value : values)
        {
            p = value.toString();
            path = p.split("\\s+");

            // check if path beginning and end match targetid1 and targetid2 respectively
            boolean goodPath = false;
            if (targetid1.contains(path[0]) && targetid2.contains(path[path.length - 1]))
            {
                // set a flag to not include path in path expansion
                goodPath = true;
                System.out.println(p);

                // write to file though
                context.write(key, value);
            }

            // write adjacency paths and add to adjacenct list
            if (targetid1.contains(path[0]) == false)
            {
                adjacent.add(p);
                context.write(key, value);
            }
            else if (!goodPath)
            {
                // not an adjacent path and not a valid path from start to end destination, add to paths
                paths.add(p);
            }
        }

        // build longer paths O(n^2)
        String[] path1, path2;
        String result = ""; // store extended path
        Text val = new Text(); // store result in Text format
        // System.out.println("=============================");
        for(String p1 : paths)
        {
            path1 = p1.split("\\s+");
            // p1 = path to expand
            for (String p2 : adjacent)
            {
                path2 = p2.split("\\s+");
                if (path1[path1.length - 1].equals(path2[0]))
                {
                    // add path2 to the end of path1
                    result = "";
                    for (int k = 0; k < path1.length; k++)
                    {
                        result = result + path1[k] + " ";
                    }
                    
                    // start at k=1 to skip adding duplicate value since end of path1 == beginning of path2
                    for (int k = 1; k < path2.length; k++)
                    {
                        result = result  + path2[k] + " ";
                    }

                    result = result.trim();
                    val.set(result);
                    context.write(key, val);
                }
            }
        }
        // System.out.println("=============================");
    }
}