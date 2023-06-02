import javax.management.modelmbean.InvalidTargetObjectTypeException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.fs.Path;

public class QSeven4 {
    public static void main(String[] args) throws Exception
    {
        Configuration conf = new Configuration();
        int rounds = Integer.parseInt(args[0]);
        for (int i = 1; i <= (rounds * 2) + 1; i++)
        {
            String input = "untranslated" + "-" + (i - 1);
            String output = "untranslated" + "-" + (i);

            conf.set("round", Integer.toString(i));

            Job job = Job.getInstance(conf, "QSeven4");
            job.setJarByClass(QSeven4.class);
            job.setMapperClass(QSevenMapper4.class);
            job.setReducerClass(QSevenReducer4.class);
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(Text.class);
            FileInputFormat.addInputPath(job, new Path(input));
            if (i % 2 == 1)
            {
                FileInputFormat.addInputPath(job, new Path("airports"));
            }
            else
            {
                FileInputFormat.addInputPath(job, new Path("airlines"));
            }
            FileOutputFormat.setOutputPath(job, new Path(output));
            job.waitForCompletion(true);
        }
    }
}