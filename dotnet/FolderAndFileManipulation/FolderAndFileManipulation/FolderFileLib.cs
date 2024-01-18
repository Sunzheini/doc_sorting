using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace FolderAndFileManipulation
{
    public class FolderFileLib
    {
        private string _testDirectory;
        //private string _testDirectory = "C:\\Appl\\Projects\\C#\\FolderAndFileManipulation\\FolderAndFileManipulation\\test";

        public FolderFileLib(string default_dir)
        {
            this._testDirectory = default_dir;
        }

        public void createDirectory(string addPth)
        {
            string newPath = Path.Combine(_testDirectory, addPth);
            Directory.CreateDirectory(newPath);
        }

        public void deleteDirectory(string addPth)
        {
            string newPath = Path.Combine(_testDirectory, addPth);
            Directory.Delete(newPath, true);  // true == delete recursive
        }

        public string getFilesInDirectory(string addPth)
        {
            string newPath = Path.Combine(_testDirectory, addPth);
            string[] files = Directory.GetFiles(newPath);

            string result = "";
            foreach (string file in files)
            {
                FileInfo info = new FileInfo(file);     // File Info!
                result += info.Name +
                    info.Extension +
                    info.Length +
                    info.CreationTime +
                    info.LastAccessTime +
                    info.LastWriteTime +
                    info.Directory +
                    info.DirectoryName;
            }
            return result;
        }

        public string getDirectoriesInDirectory(string addPth)
        {
            string newPath = Path.Combine(_testDirectory, addPth);
            string[] directories = Directory.GetDirectories(newPath);

            string result = "";
            foreach (string directory in directories)
            {
                DirectoryInfo info = new DirectoryInfo(directory);     // Directory Info!
                result += info.Name +
                    info.FullName +
                    info.CreationTime +
                    info.LastAccessTime +
                    info.LastWriteTime +
                    info.Parent;
            }
            return result;
        }

        public void MoveDirectory(string addPth, string addPth2)
        {
            string newPath = Path.Combine(_testDirectory, addPth);
            string newPath2 = Path.Combine(_testDirectory, addPth2);
            Directory.Move(newPath, newPath2);
        }
    }
}
